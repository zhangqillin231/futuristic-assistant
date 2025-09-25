class ChatService {
    private apiUrl: string;

    constructor() {
        this.apiUrl = 'https://api.openai.com/v1/chat/completions'; // Example for OpenAI
    }

    public async sendMessage(message: string): Promise<string> {
        // Replace 'YOUR_OPENAI_API_KEY' with your actual API key
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_OPENAI_API_KEY',
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [{ role: 'user', content: message }],
            }),
        });
        const data = await response.json();
        return data.choices?.[0]?.message?.content || 'No response';
    }
}

export const chatService = new ChatService();