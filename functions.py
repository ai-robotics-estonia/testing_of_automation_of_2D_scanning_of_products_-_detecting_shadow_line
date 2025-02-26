import glob
import cv2
import numpy as np
import ezdxf
import os

# Define applied filters
filter_gray = True #May set false only for debbuging
filter_contrastBoost = True #contrast adjustment
filter_contrastBoost_contrast = 1 #Contrast control (0.5-3.0). 1.0 means no change, higher values increase contrast.
filter_contrastBoost_brightness = 0 #Brightness control (-100 to 100). 0 means no change, higher values increase brightness.
filter_CannyEdgeDetection = True #defines the outline of the part by contrast
filter_Make_Contours_Continuous = True #fixes caps created by cannyEdgeDetector #check 
filter_Remove_Non_Connected_Lines = True #filters lines that are to short and thus are not part of part outline
filter_Remove_Non_Connected_Lines_min_length = 100 #smalest line length not filterd
filter_clear_larger_contours_inside = True # removes lines inside the outline
filter_clear_larger_contours_inside_min_contour_area = 5000 #smalest detail size not filterd
filter_line_reduction_simplification = True #enables to simplyfy the line 
filter_line_reduction_simplification_min_length = 0 #describes minimum line length that is alow trough the filter
filter_line_reduction_simplification_epsilon = 0.0005 #bigger the epsilon the more simplyfied the detail
filter_rectangle_epsilon = 0.005

# Define applied actions
display_images = False
display_images_time = 1 #in ms, display_images_time > 0
display_images = False
display_images_time = 0 #in ms, display_images_time > 0
display_images_scale = 0.5 #in double
save_images = False
save_outline = True
make_overlay = True

# Define directories

input_dir = "NaidisPildid/pilt-foto.jpg"
output_dir = "Katsetused"

def clear_folder(folder_path):
    try:
        # Ensure the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return

        # Find all .jpeg and .dxf files in the folder
        file_types = ["*.jpeg", "*.dxf"]
        for file_type in file_types:
            files = glob.glob(os.path.join(folder_path, file_type))
            
            # Delete each file found
            for file in files:
                try:
                    os.remove(file)
                    print(f"Deleted file: {file}")
                except Exception as e:
                    print(f"Error deleting file {file}: {e}")

    except Exception as e:
        print(f"Error in clear_folder: {e}")




def display_image(img, title, scale=display_images_scale, delay=display_images_time):
    try:
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        dim = (width, height)
        resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow(title, resized_img)
        cv2.waitKey(delay)
        cv2.destroyWindow(title)
    except Exception as e:
        print(f"Error in display_image: {e}")

def save_image(image, step_number, image_name, extension='jpeg'):
    try:
        filename = os.path.join(output_dir, f"s{step_number}_{image_name}.{extension}")
        cv2.imwrite(filename, image)
        print(f"Image saved as: {filename}")
    except Exception as e:
        print(f"Error in save_image: {e}")


def save_outline_to_dxf(image, filename, scale=1.0):
    try:
        doc = ezdxf.new()
        msp = doc.modelspace()

        # Check if the image is already grayscale
        if len(image.shape) == 2:  # Grayscale image
            binary_image = image
        else:  # Convert to grayscale if it's a color image
            _, binary_image = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            scaled_contour = [(int(point[0][0] * scale), int(point[0][1] * scale)) for point in contour]
            for i in range(len(scaled_contour) - 1):
                start_point = scaled_contour[i]
                end_point = scaled_contour[i + 1]
                msp.add_line(start=start_point, end=end_point)
        doc.saveas(filename)
    except Exception as e:
        print(f"Error in save_outline_to_dxf: {e}")

def apply_gray_filter(image):
    try:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if display_images:
            display_image(gray_image, 'Grayscale Image')
        if save_images:
            save_image(gray_image, step_number=1, image_name="grayscale_image")
        return gray_image
    except Exception as e:
        print(f"Error in apply_gray_filter: {e}")
        return image  # Return the original image if an error occurs
    
def boost_contrast(image, alpha=filter_contrastBoost_contrast, beta=filter_contrastBoost_brightness):
    try:
        # Apply contrast and brightness adjustments
        contrast_enhanced_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        
        # Display the contrast-enhanced image
        if display_images:
            display_image(contrast_enhanced_image, f'Contrast Enhanced Image (alpha={alpha}, beta={beta})')
        
        # Save the contrast-enhanced image
        if save_images:
            save_image(contrast_enhanced_image, step_number=2, image_name=f"contrast_adjusted_image")

        return contrast_enhanced_image
    
    except Exception as e:
        print(f"Error in boost_contrast: {e}")
        return image  # Return the original image if an error occurs

def apply_CannyEdgeDetection(image, threshold1=100, threshold2=200):
    try:
        edges = cv2.Canny(image, threshold1=threshold1, threshold2=threshold2, L2gradient=True)
        return edges
    except Exception as e:
        print(f"Error in apply_CannyEdgeDetection: {e}")
        return image  # Return the original image if an error occurs

def apply_make_contours_continuous(image):
    try:

        # Convert the grayscale image to binary
        _, binary_image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)

        # Define a kernel for morphological operations
        kernel = np.ones((5,5), np.uint8)

        # Apply dilation to make contours continuous
        continuous_contours = cv2.dilate(binary_image, kernel, iterations=1)

        # Display the continuous contours
        if display_images:
            display_image(continuous_contours, 'Continuous Contours Image')

        # Save the continuous contours image
        if save_images:
            save_image(continuous_contours, step_number=4, image_name="continuous_contours")

        return continuous_contours

    except Exception as e:
        print(f"Error in make_contours_continuous: {e}")
        return image  # Return the original image if an error occurs
    
def apply_remove_nonConected_lines(image, min_length=filter_Remove_Non_Connected_Lines_min_length):
    try:
        # Convert the grayscale image to binary
        _, binary_image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)

        # Find all contours
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a blank image to draw the filtered contours
        filtered_image = np.zeros_like(binary_image)

        for contour in contours:
            # Calculate the contour length
            length = cv2.arcLength(contour, closed=False)

            # Filter contours based on length
            if length >= min_length:
                cv2.drawContours(filtered_image, [contour], -1, (255, 255, 255), thickness=1, lineType= cv2.LINE_4)

        # Display the processed image
        if 'display_images' in globals() and display_images:
            display_image(filtered_image, 'remove nonConected lines')

        # Save the processed image
        if 'save_images' in globals() and save_images:
            save_image(filtered_image, step_number=5, image_name="remove_nonConected_lines")

        return filtered_image

    except Exception as e:
        print(f"Error in remove_short_lines: {e}")
        return image  # Return the original image if an error occurs

    
def apply_clear_larger_contours_inside(image, min_contour_area=filter_clear_larger_contours_inside_min_contour_area):

    try:
        # Convert grayscale image to binary
        _, binary_image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)

        # Find all contours
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if any contours were found
        if not contours:
            print("No contours found.")
            return image

        # Create a blank image to draw the filtered contours
        filtered_image = np.zeros_like(image)

        for contour in contours:
            # Calculate the area of each contour
            area = cv2.contourArea(contour)

            # Filter contours based on area
            if area >= min_contour_area:
                cv2.drawContours(filtered_image, [contour], -1, (255, 255, 255), thickness= 1, lineType= cv2.LINE_4)

        # Display the processed image
        if display_images:
            display_image(filtered_image, 'object cleared inside')

        # Save the processed image
        if save_images:
            save_image(filtered_image, step_number=6, image_name="object_cleared_inside")

        return filtered_image

    except Exception as e:
        print(f"Error in apply_clear_larger_contours: {e}")
        return image  # Return the original image if an error occurs
    

def apply_line_reduction_simplification(image, min_length=filter_line_reduction_simplification_min_length, epsilon=filter_line_reduction_simplification_epsilon):#

    try:
        # Convert the grayscale image to binary
        _, binary_image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)

        # Find all contours
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a blank image to draw the simplified contours
        reduced_image = np.zeros_like(image)

        for contour in contours:
            # Simplify the contour
            epsilon_scaled = epsilon * cv2.arcLength(contour, True)  # Scale epsilon by the contour length
            simplified_contour = cv2.approxPolyDP(contour, epsilon_scaled, True)
            
            # Draw simplified contour as lines
            if len(simplified_contour) > 1:
                for i in range(len(simplified_contour)):
                    start_point = tuple(simplified_contour[i][0])
                    end_point = tuple(simplified_contour[(i + 1) % len(simplified_contour)][0])
                    line_length = np.linalg.norm(np.array(start_point) - np.array(end_point))
                    if line_length > min_length:
                        cv2.line(reduced_image, start_point, end_point, (255, 255, 255), thickness=1, lineType= cv2.LINE_4)

        # Display the result image
        if display_images:
            display_image(reduced_image, 'Simplified and Reduced Lines Image')

        # Save the result image
        if save_images:
            save_image(reduced_image, step_number=7, image_name="simplified_reduced_lines")

        return reduced_image

    except Exception as e:
        print(f"Error in simplify_and_reduce_lines: {e}")
        return image  # Return the original image if an error occurs


def toggle_rectangle_view(image, num_corners, epsilon=filter_rectangle_epsilon):
    try:
        # Convert the image to grayscale if it's not already
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Convert the grayscale image to binary
        _, binary_image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)

        # Find all contours
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Create a blank mask to draw the polygons
        polygon_mask = np.zeros_like(binary_image)

        for contour in contours:
            # Compute the convex hull of the contour
            hull = cv2.convexHull(contour)

            # Get initial epsilon for simplification
            epsilon_scaled = epsilon * cv2.arcLength(hull, True)
            reduced_polygon = cv2.approxPolyDP(hull, epsilon_scaled, True)

            # Adjust corners dynamically to achieve the desired count
            max_iterations = 50  # Set a maximum number of iterations to prevent infinite loops
            iteration = 0

            while len(reduced_polygon) != num_corners:
                iteration += 1

                if len(reduced_polygon) > num_corners:
                    epsilon_scaled *= 1.05  # Increase tolerance to reduce corners
                else:
                    epsilon_scaled *= 0.95  # Decrease tolerance to add corners

                reduced_polygon = cv2.approxPolyDP(hull, epsilon_scaled, True)

                if abs(len(reduced_polygon) - num_corners) <= 1 or iteration >= max_iterations:
                    break

            # Draw the polygon for the current contour
            cv2.drawContours(polygon_mask, [reduced_polygon], -1, (255), thickness=2)

        # Convert the mask to BGR format for display
        processed_image = cv2.cvtColor(polygon_mask, cv2.COLOR_GRAY2BGR)

        return processed_image

    except Exception as e:
        print(f"Error in toggle_rectangle_view: {e}")
        return image  # Return the original image if an error occurs
