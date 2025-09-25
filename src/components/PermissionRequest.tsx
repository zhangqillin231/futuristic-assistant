import React, { useEffect } from 'react';
import { Button, View, Text } from 'react-native';
import { requestPermissions } from '../services/permissionService';

const PermissionRequest = () => {
    useEffect(() => {
        requestPermissions();
    }, []);

    return (
        <View>
            <Text>Requesting permissions for microphone, camera, and storage...</Text>
            <Button title="Retry Permissions" onPress={requestPermissions} />
        </View>
    );
};

export default PermissionRequest;