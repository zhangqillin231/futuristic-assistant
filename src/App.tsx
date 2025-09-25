
import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import SplashScreen from './components/SplashScreen';
import ChatInterface from './components/ChatInterface';
import './styles/futuristic.css';
import ConsentModal from './components/ConsentModal';

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [consentOpen, setConsentOpen] = useState(false);
  const [consentPayload, setConsentPayload] = useState({title:'', description:'', onConfirm: ()=>{}, onCancel: ()=>{}});

  const handleActionProposal = (title, description, onConfirm) => {
    setConsentPayload({title, description, onConfirm, onCancel: ()=>setConsentOpen(false)});
    setConsentOpen(true);
  };

  return (
    <div className="app-root">
      {showSplash && <SplashScreen onDone={()=>setShowSplash(false)} />}
      {!showSplash && <div className="app-main">
        <header className="topbar">
          <div className="brand">2050 Assistant</div>
          <div className="status">Ready</div>
        </header>
        <main className="main-area">
          <aside className="sidebar">Connected devices will appear here.</aside>
          <section className="chat-area">
            <ChatInterface onProposal={handleActionProposal} />
          </section>
        </main>
      </div>}
      <ConsentModal open={consentOpen} title={consentPayload.title} description={consentPayload.description} onConfirm={()=>{consentPayload.onConfirm(); setConsentOpen(false);}} onCancel={()=>{consentPayload.onCancel(); setConsentOpen(false);}} />
    </div>
  );
}

export default App;
