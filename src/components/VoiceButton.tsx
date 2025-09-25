
import React from 'react';

export default function VoiceButton({ onStart }: { onStart: () => void }) {
  return (
    <button className="voice-btn" onClick={onStart} aria-label="Start voice">
      <svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 14a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v5a3 3 0 0 0 3 3z"/></svg>
    </button>
  );
}
