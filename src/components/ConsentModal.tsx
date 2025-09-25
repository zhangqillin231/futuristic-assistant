
import React from 'react';

export default function ConsentModal({ open, title, description, onConfirm, onCancel }: { 
  open: boolean, title: string, description: string, onConfirm: () => void, onCancel: () => void }) {
  if (!open) return null;
  return (
    <div className="consent-backdrop">
      <div className="consent-card">
        <h3>{title}</h3>
        <p>{description}</p>
        <div className="consent-actions">
          <button className="btn-deny" onClick={onCancel}>Deny</button>
          <button className="btn-confirm" onClick={onConfirm}>Confirm</button>
        </div>
      </div>
    </div>
  );
}
