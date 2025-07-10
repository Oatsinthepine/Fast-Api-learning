import { useState } from "react"

/*
* This FileForm component is he practice of uploading files from a React frontend to fast api backend server.
* Then once the file is selected and user click the upload button, the file will be sent to the backend server using fetch API via POSt request.
* Then the backend server will handle the file upload and save it to the specified directory, in this exercise, the uploaded file will be send to /FastAPI_Learning/uploads directory.
*/

export default function FileForm() {
    // State to hold the selected file
    const [file, setFile] = useState <File | null>(null);
    // this function handles the file selection event
    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selected_file = event.target.files?.[0];
        if (selected_file) {
            console.log("File selected:", selected_file.name);
            // update the file state to the selected file
            setFile(selected_file)
        }
    }
    // this function handles the file upload event
    const uploadFile = async (event: any) => {
        event.preventDefault();
        if (!file) {
            console.log("Please select a file to upload.");
            return;
        }
        // create a new FormData object and append the selected file to it
        // new FormData creates a new instance of the FormData class, used to handle data directly from HTML forms and allows you to easily construct and send data to the server via AJAX or fetch requests.
        const formData = new FormData();
        // Here we must ensure key "file_uploaded" match the fast api end point parameter name, which is `async def create_upload_file(file_uploaded: UploadFile)`
        formData.append("file_uploaded", file)
        // Then using try catch block for the fetch request to upload the file to the backend server
        try {
            // point to the backend server api endpoint where the file will be uploaded
            const endpoint = "http://localhost:8000/upload_file";
            // use fetch API to send a POST request to the backend server with the FormData object
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData,
            })
            if (response.ok) {
                console.log("File uploaded successfully");
            } else {
                console.error("File upload failed:", response.statusText);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    }

    return (
        <div>
            <h1>Upload File</h1>
            <form>
                <input type ="file" onChange={handleFileUpload}/>
                <button type="submit" onSubmit={uploadFile}>Upload</button>
            </form>
        {/* just checking the uploaded file name(for debug purpose}*/}
            {file && <p>Selected file: {file.name}</p>}
        </div>
    )
}