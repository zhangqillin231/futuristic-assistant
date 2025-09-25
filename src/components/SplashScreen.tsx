
import React, { useEffect, useState } from 'react';
import OrbAvatar from './OrbAvatar';

export default function SplashScreen({ onDone }: { onDone: () => void }) {
  const [phase, setPhase] = useState(0);
  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 900);
    const t2 = setTimeout(() => setPhase(2), 2200);
    const t3 = setTimeout(() => { setPhase(3); setTimeout(onDone, 900); }, 3600);
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); };
  }, []);

  return (
    <div className="splash-root">
      <div className="splash-card">
        <OrbAvatar speaking={phase>1} />
        <div className="splash-text">
          <div className="splash-title">2050 Assistant</div>
          <div className="splash-sub">Booting neural cores · {phase}/3</div>
        </div>
        <div className={'splash-progress p'+phase}></div>
      </div>
    </div>
  );
}
