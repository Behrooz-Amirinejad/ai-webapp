import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatUploader.css';

export default function ChatUploader() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState('');
  const chatEndRef = useRef(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [fileType, setFileType] = useState('');


  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatLog]);



  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const res = await axios.post('http://localhost:8080/upload', formData);
      setUploadMsg(res.data.message || 'Upload successful.');
    } catch (err) {
      console.error(err);
      setUploadMsg('An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) return;

    const currentQ = question.trim();
    setChatLog((prev) => [...prev, { type: 'user', text: currentQ }]);
    setQuestion('');
    try {
      setLoading(true);
      const res = await axios.post('http://localhost:8080/ask', { question: currentQ });
      setChatLog((prev) => [...prev, { type: 'assistant', text: res.data.answer }]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

const handleFileChange = async (e) => {
  const selectedFile = e.target.files[0];
  if (!selectedFile) return;

  setFile(selectedFile);
  setUploadMsg('');
  setFileType(selectedFile.type);

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    setLoading(true);
    const res = await axios.post('http://localhost:8080/upload', formData);
    setUploadMsg(res.data.message || 'Upload successful.');

    // Set preview for image/pdf
    const localUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(localUrl);
  } catch (err) {
    console.error(err);
    setUploadMsg('An error occurred.');
  } finally {
    setLoading(false);
  }
};
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="chat-container d-flex flex-column align-items-center justify-content-between min-vh-100 p-4">

      {/* Centered welcome message */}
      <div className="text-center my-4">
        <h2 className="fw-bold">Text Analyser</h2>
        <p className="text-muted fs-5">Upload your time and then inquery</p>
      </div>

      {/* File Upload Section */}


      {/* Chat Box */}
      <div className="flex-grow-1 w-100 overflow-auto px-2" style={{ maxWidth: '700px', marginBottom: '90px' }}>
        {chatLog.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-bubble ${msg.type === 'user' ? 'user' : 'assistant'}`}
          >
            {msg.text}
          </div>
        ))}

        <div ref={chatEndRef}></div>
      </div>

      {/* Input fixed to bottom */}
      <div className="chat-input-section w-100 fixed-bottom py-3 px-3 bg-dark" style={{ maxWidth: '700px', margin: '0 auto' }}>
        <div className="input-group">

          {/* Upload Image Icon */}
          <label htmlFor="file-upload" className="input-group-text bg-secondary border-0" style={{ cursor: 'pointer' }}>
            <img src="/static/img/upload_icon.png" alt="Upload" width="24" />
          </label>
          <input
            id="file-upload"
            type="file"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />

          {/* Question Input */}
          <input
            type="text"
            className="form-control"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Send a message..."
            disabled={loading}
          />

          {/* Ask Button */}
          <button className="btn btn-primary" onClick={askQuestion} disabled={loading}>
            Ask
          </button>
        </div>

        {/* Upload Message */}
        {uploadMsg && <div className="text-success text-center mt-2">{uploadMsg}</div>}
      </div>


      {/* Loading spinner */}
      {loading && (
        <div className="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center bg-white bg-opacity-75">
          <div className="spinner-border text-primary" role="status" />
        </div>
      )}

      {/* hiding the upload form */}
      {/* <form onSubmit={handleUpload} className="w-100" style={{ maxWidth: '600px' }} encType="multipart/form-data">
        <div className="input-group mb-3">
          <label htmlFor="file-upload" style={{ cursor: 'pointer' }} className="me-2">
            <img src="/static/img/upload_icon.png" alt="Upload" width="40" />
          </label>
          <input
            id="file-upload"
            type="file"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          {file && (
            <button className="btn btn-secondary" type="submit">
              Upload
            </button>
          )}
        </div>
        {uploadMsg && <div className="text-success text-center">{uploadMsg}</div>}
      </form> */}

    </div>
  );
}
