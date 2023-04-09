import streamlit as st
import zipfile
import io

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

                    try:
                    # Loop through each section
                        for section in data['sections']:
                            # Loop through each visualContainer
                            for visualContainer in section['visualContainers']:
                                # Check if y is 0 and config contains "parallelogram"
                                if "parallelogram" in visualContainer['config'] :
                                    # Remove the visualContainer
                                    section['visualContainers'].remove(visualContainer)
                    except:
                        print('hi')
                    # Add the manipulated layout data to the destination zip file
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
