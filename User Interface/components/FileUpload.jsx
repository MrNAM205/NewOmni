import React, { useState } from 'react';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [analysis, setAnalysis] = useState(null);
    const [error, setError] = useState(null);

    const onFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const onFileUpload = () => {
        if (!file) {
            setError("Please select a file first.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('http://localhost:5001/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                setError(data.error);
                setAnalysis(null);
            } else {
                setAnalysis(data);
                setError(null);
            }
        })
        .catch(error => {
            setError(error.toString());
            setAnalysis(null);
        });
    };

    return (
        <div>
            <h2>Document Upload and Analysis</h2>
            <div>
                <input type="file" onChange={onFileChange} />
                <button onClick={onFileUpload}>
                    Upload and Analyze
                </button>
            </div>
            {error && <div style={{ color: 'red', marginTop: '10px' }}>Error: {error}</div>}
            {analysis && (
                <div style={{ marginTop: '20px', whiteSpace: 'pre-wrap', border: '1px solid #ccc', padding: '10px' }}>
                    <h3>Analysis Result</h3>
                    <pre>{JSON.stringify(analysis, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
