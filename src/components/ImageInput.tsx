import React from 'react';
import { Button } from 'react-native';
import { pickImageAndAnalyze } from '../services/imageService';

const ImageInput = ({ onImageResult }: { onImageResult: (desc: string) => void }) => {
    const handleImage = async () => {
        const description = await pickImageAndAnalyze();
        if (description) onImageResult(description);
    };

    return <Button title="Send Image" onPress={handleImage} />;
};

export default ImageInput;