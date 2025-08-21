import React from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

function Home() {
  const navigate = useNavigate();
  return (
    <div className="home-container">
      <div className="home-card">
        <h1>
          <span style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px'}}>
            <svg width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="6" y="6" width="26" height="26" rx="8" fill="#43cea2"/>
              <path d="M19 12C22.3137 12 25 14.6863 25 18C25 21.3137 22.3137 24 19 24C15.6863 24 13 21.3137 13 18C13 14.6863 15.6863 12 19 12Z" fill="#185a9d"/>
              <rect x="15" y="17" width="8" height="7" rx="3.5" fill="#fff"/>
            </svg>
            Mindcraft Lab: PII Masking App
          </span>
        </h1>
        <p>
          This project automatically detects and masks Personally Identifiable Information (PII) from ID images using advanced OCR and AI techniques. Upload your ID image and let the app protect your privacy by hiding sensitive details like name, address, Aadhaar, phone, email, and date of birth.
        </p>
        <button className="get-started-btn" onClick={() => navigate('/upload')}>Get Started</button>
      </div>
    </div>
  );
}

export default Home;
