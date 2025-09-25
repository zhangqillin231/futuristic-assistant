import React, { useState } from 'react';
import { View, TextInput as RNTextInput, Button, StyleSheet } from 'react-native';

const TextInput = ({ onSubmit }: { onSubmit: (text: string) => void }) => {
    const [inputValue, setInputValue] = useState('');

    const handleChange = (text: string) => setInputValue(text);

    const submitInput = () => {
        if (inputValue.trim()) {
            onSubmit(inputValue);
            setInputValue('');
        }
    };

    return (
        <View style={styles.container}>
            <RNTextInput
                style={styles.input}
                value={inputValue}
                onChangeText={handleChange}
                placeholder="Type your message..."
                placeholderTextColor="#888"
            />
            <Button title="Send" onPress={submitInput} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
    input: { flex: 1, backgroundColor: '#222', color: '#fff', padding: 8, borderRadius: 8, marginRight: 8 },
});

export default TextInput;