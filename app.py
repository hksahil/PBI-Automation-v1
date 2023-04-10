# Condition that removes all the rectangles and parallelograms except the first parallelogram

import streamlit as st
import zipfile
import io
import json

st.title('Automate your PBIX file')

# Upload the source zip file
ss = st.file_uploader('Upload a PBIX file')

# --------- Removing Streamlit's Hamburger and Footer starts ---------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            a {text-decoration: none;}
            .css-15tx938 {font-size: 18px !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --------- Removing Streamlit's Hamburger and Footer ends ------------

if ss:
    # In-memory byte stream to hold the destination zip file data
    zip_data = io.BytesIO()

    # Extract the files from the source zip file and re-zip them into a destination zip file
    with zipfile.ZipFile(ss, 'r') as source_zip:
        with zipfile.ZipFile(zip_data, 'w') as destination_zip:
            # Iterate over the files in the source zip file
            for name in source_zip.namelist():

                # Skip the Security Binding file
                if name == 'SecurityBindings':
                    continue

                # Manipulate the Layout file
                if name == 'Report/Layout':
                    # Read the contents of the layout file
                    data = source_zip.read(name).decode('utf-16 le')

                    # Old layout file
                    with open('og_file.json', 'w') as f:
                        a=json.loads(data)
                        json.dump(a, f)
                    try:
                        ##### Removing certain elements
                        data=json.loads(data)
                        for section in data['sections']:
                            print(section)

                            # Create a new list of visual containers that don't meet the condition
                            new_visual_containers = []
                            for visualContainer in section['visualContainers']:
                                # Check if y is 0 and x is >500 and config contains "parallelogram" or "rectangle"
                                if visualContainer['y'] == 0 and visualContainer['x'] > 500 and ("parallelogram" in visualContainer['config'] or "rectangle" in visualContainer['config']):
                                    continue
                                else:
                                    new_visual_containers.append(visualContainer)

                            # Replace the old list with the new list
                            section['visualContainers'] = new_visual_containers
                        
                        ##### Changing attributes of certain elements
                        for section in data['sections']:
                            for visualContainer in section['visualContainers']:

                                # Changing Header rectangle
                                if visualContainer['y'] == 0 and "#004E90" in visualContainer['config'] :
                                    # Change x, height, and width
                                    visualContainer['x'] = 0
                                    visualContainer['height'] = 65
                                    visualContainer['width'] = 1280
                                    # Change config
                                    config = json.loads(visualContainer['config'])

                                    # Parallelogram to Rectangle
                                    # Replace "parallelogram" with "rectangle" in the "config" key's value
                                    config["singleVisual"]["objects"]["shape"][0]["properties"]["tileShape"]["expr"]["Literal"]["Value"] = "'rectangle'"

                                    for layout in config['layouts']:
                                        layout['position']['x'] = 0
                                        layout['position']['height'] = 65
                                        layout['position']['width'] = 1280 
                                    visualContainer['config'] = json.dumps(config)

                                # Changing z of logo
                                if visualContainer['y'] == 0 and "Pepsico_4659666136978873.png" in visualContainer['config']:
                                    visualContainer['z'] = 50000
                                    # Change config
                                    config = json.loads(visualContainer['config'])
                                    for layout in config['layouts']:
                                        layout['position']['z'] = 50000
                                    visualContainer['config'] = json.dumps(config)

                                # Changing attributes of groups
                                if visualContainer['y'] == 0 and "singleVisualGroup" in visualContainer['config']:
                                    visualContainer['x'] = 0
                                    visualContainer['height'] = 65
                                    visualContainer['width'] = 1280
                                    # Change config
                                    config = json.loads(visualContainer['config'])
                                    for layout in config['layouts']:
                                        layout['position']['x'] = 0
                                        layout['position']['height'] = 65
                                        layout['position']['width'] = 1280
                                    visualContainer['config'] = json.dumps(config)
                        
                        # New Layout file
                        with open('updated_file.json', 'w') as f:
                            json.dump(data, f)
                    
                    except:
                        print('hi')
                    # Add the manipulated layout data to the destination zip file
                    data = json.dumps(data)
                    destination_zip.writestr(name, data.encode('utf-16 le'))
                
                else:
                    # Add the file to the destination zip file as-is
                    binary_data = source_zip.read(name)
                    destination_zip.writestr(name, binary_data)


    # Download the destination file
    st.download_button(
        label='Download Destination PBIX File',
        data=zip_data.getvalue(),
        file_name='destination.pbix',
        mime='application/pbix'
    )
else:
    
    st.warning('Please upload a pbix file')
