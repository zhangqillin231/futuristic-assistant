
import React from 'react';

export default function OrbAvatar({ speaking = false }: { speaking?: boolean }) {
  const glow = speaking ? 'orb-glow-speaking' : 'orb-glow';
  return (
    <div className={'orb-container ' + glow} aria-hidden>
      <div className="orb-core"></div>
      <svg className="orb-rings" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="30" fill="none" stroke="rgba(126,252,154,0.08)" strokeWidth="0.8"/>
        <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(110,191,255,0.04)" strokeWidth="0.6"/>
      </svg>
    </div>
  );
}
