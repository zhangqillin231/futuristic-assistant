import React, { useEffect } from 'react';
import { PermissionsAndroid, Button, View, Text } from 'react-native';
import { requestPermissions as requestPermissionsAPI } from './path-to-your-permission-module'; // Adjust the import based on your file structure

const PermissionRequest = () => {
    const requestPermissions = async () => {
        try {
            await requestPermissionsAPI();
        } catch (err) {
            console.warn(err);
        }
    };

    useEffect(() => {
        requestPermissions();
    }, []);

    return (
        <View>
        <Text>Requesting permissions for microphone, camera, and storage...</Text>
            < Button title = "Retry Permissions" onPress = { requestPermissions } />
                </View>
    );
};

export default PermissionRequest;