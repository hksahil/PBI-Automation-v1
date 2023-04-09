import streamlit as st
import zipfile
import io
import json

st.title('Automate your PBIX file')

# Upload the source zip file
ss = st.file_uploader('Upload a PBIX file')

if ss:
    # In-memory byte stream to hold the destination zip file data
    zip_data = io.BytesIO()

    # Extract the files from the source zip file and re-zip them into a destination zip file
    with zipfile.ZipFile(ss, 'r') as source_zip:
        with zipfile.ZipFile(zip_data, 'w') as destination_zip:
            # Iterate over the files in the source zip file
            for name in source_zip.namelist():

                # Skip the Security Binding file
                if name=='SecurityBindings':
                    continue

                # Manipulate the Layout file
                if name == 'Report/Layout':
                    # Read the contents of the layout file
                    data = source_zip.read(name).decode('utf-16 le')
                    print(data,'data')

                    # Old layout file
                    with open('og_file.json', 'w') as f:
                            a=json.loads(data)
                            json.dump(a, f)
                    try:
                    # Loop through each section
                        data=json.loads(data)
                        for section in data['sections']:
                            print(section)

                            # Loop through each visualContainer
                            for visualContainer in section['visualContainers']:
                                # Check if y is 0 and config contains "parallelogram"
                                if visualContainer['y'] == 0 and ( "parallelogram" in visualContainer['config'] or "rectangle" in visualContainer['config']) :
                                    # Remove the visualContainer
                                    section['visualContainers'].remove(visualContainer)
                        
                        # new layout file
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
