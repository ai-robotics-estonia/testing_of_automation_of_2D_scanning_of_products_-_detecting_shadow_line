*This is a template repository for this organization. Start by replacing the placeholder for the project name with its actual title.*

# [Demonstration Project title]

## Summary
| Company Name | [Company](https://website.link) |
| :--- | :--- |
| Development Team Lead Name | [Dr. John Smith](https://profile.link) |
| Development Team Lead E-mail | [email@example.com](mailto:email@example.com) |
| Duration of the Demonstration Project | month/year-month/year |
| Final Report | [Example_report.pdf](https://github.com/ai-robotics-estonia/_project_template_/files/13800685/IC-One-Page-Project-Status-Report-10673_PDF.pdf) |

### Each project has an alternative for documentation
1. Fill in the [description](#description) directly in the README below *OR*;
2. make a [custom agreement with the AIRE team](#custom-agreement-with-the-AIRE-team).

# Description
## Objectives of the Demonstration Project
*Please describe your project objectives in detail.*

The aim of the project is to test a cost-effective device concept that automates the preparatory design stage of production. The device would help reduce the amount of manual work and decrease the time required to obtain the shadow outline of packaged products/equipment. Additionally, it would improve work quality by enhancing the accuracy of results.

The 2D scanning/shadow outline detection of a product or component is currently a manual and time-consuming process, and no suitable devices are available on the market to simplify and automate this process.The need for a device that speeds up and simplifies this task extends across various industries, creating opportunities to commercialize the developed device.

## Activities and Results of the Demonstration Project
### Challenge
*Please describe challenge addressed (i.e, whether and how the initial challenge was changed during the project, for which investment the demonstration project was provided).*

The company's production capacity has significantly improved over time, largely due to the adoption of CNC machines. However, there is still considerable potential to enhance internal processes through digitalization, allowing for the service of an even larger customer base. Currently, a major bottleneck in production is the preparation phase, where excessive time is spent on technical documentation and measuring customer products. Automating this process would lead to a significant breakthrough in increasing production throughput and reducing delivery times for customers.

A foam plastic sheet is cut on a CNC milling machine to create a precise cavity that matches the shape of the packaged product. To generate the CNC machining program for this cavity, the product’s projection/shadow outline must be obtained.

At present, no suitable devices are available on the market for this specific purpose. Existing scanning solutions generate large data volumes with excessive unnecessary information, making the process time-consuming and expensive. Photography-based approaches introduce distortions, and some parts of the packaged product may remain hidden. Light projection methods also cause shape distortions.

The accuracy and speed of detecting the shadow outline of packaged products/equipment are crucial for creating precise and cost-effective transport cases. Currently, the 2D scanning/shadow outline detection process is manual and time-consuming, and no suitable devices exist on the market to simplify and automate it.

The goal of the project is to automatically generate a DXF drawing that can be directly used as a CNC machine command. This solution will also eliminate the time-consuming step of preparing technical documentation.

### Data Sources

- 2D Image Data (Basler Cameras via Pypylon),
- Edge Detection Algorithms (OpenCV Canny Edge),
- Lighting and Contrast Optimization Parameters,
- Ramer-Douglas-Peucker Algorithm,
- Convex Hull Algorithm,
- Contour Refinement and Noise Removal

### AI Technologies
*Please describe and justify the use of selected AI technologies.*
- [AI technology 1],
- [AI technology 2],
- etc... .

### Technological Results
*Please describe the results of testing and validating the technological solution.*

Testing has shown that the measurement accuracy of a single-camera system is approaching the required limits for objects up to xxxxx mm in height. While further refinements may be needed, initial results indicate that a single-camera setup can provide sufficient precision for contour detection. This suggests that additional optimization could help meet exact industrial requirements without the need for more complex configurations.

The choice of optical components, particularly in terms of lens distortion and focal length optimization, plays a crucial role in system performance. Testing has provided valuable insights into how different lens parameters affect accuracy. By fine-tuning optical properties, it is possible to minimize geometric distortions and enhance the reliability of the extracted contours.

A multi-camera setup, specifically a four-camera system, was evaluated but found to be unjustified compared to a single-camera approach. The mechanical complexity of aligning and synchronizing multiple cameras would require precise movement coordination, making the system overly intricate. Given these challenges, a well-calibrated single-camera setup was determined to be the more efficient and practical solution, offering similar results with significantly reduced complexity.

The brightness of the light box was tested up to a distance of 1290 mm, and results confirmed that illumination levels remain sufficient for accurate contour detection. The uniform lighting minimizes shadow interference and enhances the clarity of object edges, contributing to more precise contour extraction. These findings validate that the lighting conditions are well-suited for high-accuracy imaging within the tested range.

In conclusion, the single-camera approach proves to be both effective and practical, provided that optical parameters are carefully optimized. The multi-camera system does not offer significant advantages, given the challenges in mechanical alignment and synchronization. Additionally, the lighting setup is sufficient for maintaining accuracy at extended distances. These results guide further refinements in optical calibration and software processing, ensuring continuous improvements in system performance.

### Technical Architecture
*Please describe the technical architecture (e.g, presented graphically, where the technical solution integration with the existing system can also be seen).*
- [Component 1],
- [Component 2], 
- etc... .

![backend-architecture](flowchart.png)


### User Interface 
*Please describe the details about the user interface(i.e, how does the client 'see' the technical result, whether a separate user interface was developed, command line script was developed, was it validated as an experiment, can the results be seen in ERP or are they integrated into work process)*

The user interface for the system was designed using Tinkercad library to provide a clear and intuitive way for clients to interact with the contour detection process and access the generated technical results. The approach taken was based on the specific use case and integration needs:

Capture an image of the object using an integrated camera system. Set the camera parameters, scaling, and crop the image.
View real-time contour extraction results using edge detection and contour simplification techniques.
Adjust processing parameters, such as sensitivity, scaling, thresholding, and contour filtering, to fine-tune the output. Contourline can be optimized by amount of conrners, line shape sensitivity, consistency, removal of unconnected lines.
Export results as a DXF file, which can be used in CNC machining or other automated processes.

The UI was validated through experimental testing, where users interacted with the system to assess usability and workflow efficiency. Feedback was used to refine the interface, ensuring an intuitive experience with minimal manual intervention.

![UI](UI.png)
### Future Potential of the Technical Solution

This machine learning and computer vision solution is unique, and the developed device has market potential. In addition to optimizing production processes, the device also creates an opportunity to tap into a new market by selling the system itself.

A similar shadow outline extraction method can be applied in photo editing, object recognition, and product inspection. The use in quality control of complicated parts is also an opportunity, such as identifying defects by comparing contours to reference models.

The most straightforward use is in the same field of safety case production. Industry at its current state uses mainly manual work to produce contourlines of products and parts.

Additional uses can include robotics and automation. In object recognition and grasping the solution can be used to  assists robotic arms in identifying and picking objects in assembly lines. Autonomous robots could detect and avoid obstacles using contour analysis.


### Lessons Learned

Testing and validation have provided key insights into the effectiveness of different approaches for contour detection and DXF generation. One major takeaway is that a four-camera system with fixed positions does not justify its complexity. The challenges in mechanical alignment and synchronization outweigh the potential benefits, making a single-camera setup with optimized parameters the more efficient solution.

Another important finding is that software-based distortion correction alone is not sufficient to ensure the required level of accuracy. While computational methods can compensate for some optical distortions, they do not provide the precision necessary for high-accuracy applications. This highlights the critical importance of selecting the right optical components, as proper lens choices play a fundamental role in achieving accurate contour detection.

Finally, despite these challenges, the overall methodology has proven to be effective in solving the problem. The approach of using machine vision for automated contour extraction and DXF output is viable, and with continued refinements in optical selection and calibration, the system can achieve even higher precision and reliability.

# Custom agreement with the AIRE team
*If you have a unique project or specific requirements that don't fit neatly into the Docker file or description template options, we welcome custom agreements with our AIRE team. This option allows flexibility in collaborating with us to ensure your project's needs are met effectively.*

*To explore this option, please contact our demonstration projects service manager via katre.eljas@taltech.ee with the subject line "Demonstration Project Custom Agreement Request - [Your Project Name]." In your email, briefly describe your project and your specific documentation or collaboration needs. Our team will promptly respond to initiate a conversation about tailoring a solution that aligns with your project goals.*
