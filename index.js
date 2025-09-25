{
  "name": "chatbot-app",
    "version": "1.0.0",
      "description": "A chatbot application that combines features of ChatGPT, Siri, and Bixby with voice, text, and image input capabilities.",
        "main": "src/main.ts",
          "scripts": {
    "start": "ts-node src/main.ts",
      "build": "tsc",
        "test": "jest"
  },
  "dependencies": {
    "react": "^17.0.2",
      "react-dom": "^17.0.2",
        "typescript": "^4.4.4",
          "ts-node": "^10.4.0",
            "jest": "^27.0.6"
  },
  "devDependencies": {
    "@types/react": "^17.0.2",
      "@types/react-dom": "^17.0.2",
        "eslint": "^7.32.0",
          "eslint-config-airbnb": "^18.2.1",
            "eslint-plugin-import": "^2.24.2",
              "eslint-plugin-react": "^7.28.0",
                "eslint-plugin-react-hooks": "^4.2.0"
  },
  "keywords": [
    "chatbot",
    "voice",
    "text",
    "image",
    "AI"
  ],
    "author": "Your Name",
      "license": "MIT"
}

import { AppRegistry } from 'react-native';
import App from './src/main';
import { name as appName } from './app.json';

AppRegistry.registerComponent(appName, () => App);