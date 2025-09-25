export function formatMessage(message: string): string {
    return message.trim().replace(/\s+/g, ' ');
}

export function validateInput(input: string): boolean {
    return input.length > 0 && input.length <= 500;
}