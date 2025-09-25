export interface UserInput {
    type: 'text' | 'voice' | 'image';
    content: string | File; // For image input, content will be a File object
}

export interface ChatResponse {
    message: string;
    timestamp: Date;
    userId: string; // ID of the user who sent the message
}