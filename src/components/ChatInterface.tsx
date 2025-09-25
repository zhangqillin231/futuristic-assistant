import React, { useState } from 'react';
import { View, TextInput, Button, Text, StyleSheet } from 'react-native';
import VoiceInput from './VoiceInput';
import ImageInput from './ImageInput';
import { sendMessageToAI } from '../services/chatService';

const ChatInterface = () => {
    const [message, setMessage] = useState('');
    const [chat, setChat] = useState<string[]>([]);

    const handleSend = async (input: string) => {
        setChat([...chat, `You: ${input}`]);
        const aiResponse = await sendMessageToAI(input);
        setChat(prev => [...prev, `Bot: ${aiResponse}`]);
    };

    return (
        <View style={styles.chatContainer}>
            <View style={styles.chatBox}>
                {chat.map((msg, idx) => (
                    <Text key={idx} style={styles.chatText}>{msg}</Text>
                ))}
            </View>
            <TextInput
                style={styles.input}
                value={message}
                onChangeText={setMessage}
                placeholder="Type your message..."
                placeholderTextColor="#888"
            />
            <Button title="Send" onPress={() => { handleSend(message); setMessage(''); }} />
            <VoiceInput onVoiceResult={handleSend} />
            <ImageInput onImageResult={handleSend} />
        </View>
    );
};

const styles = StyleSheet.create({
    chatContainer: { flex: 1, padding: 16 },
    chatBox: { flex: 1, marginBottom: 8 },
    chatText: { color: '#fff', marginVertical: 2 },
    input: { backgroundColor: '#222', color: '#fff', padding: 8, borderRadius: 8, marginBottom: 8 },
});

export default ChatInterface;