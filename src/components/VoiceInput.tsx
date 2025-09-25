import React from 'react';
import { Button } from 'react-native';
import { startVoiceRecognition } from '../services/voiceService';

const VoiceInput = ({ onVoiceResult }: { onVoiceResult: (text: string) => void }) => {
    const handleVoice = async () => {
        const result = await startVoiceRecognition();
        if (result) onVoiceResult(result);
    };

    return <Button title="Speak" onPress={handleVoice} />;
};

export default VoiceInput;