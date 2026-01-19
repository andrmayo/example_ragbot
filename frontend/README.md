# Resume RAGBot Frontend

React + TypeScript frontend for the resume Q&A chatbot.

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts        # API calls to backend
│   ├── components/
│   │   ├── FileUpload.tsx   # Drag-drop or file picker
│   │   ├── ChatInput.tsx    # Question input box
│   │   ├── ChatMessage.tsx  # Single Q&A display
│   │   ├── SourceBadge.tsx  # Shows which resume was cited
│   │   └── CollectionSelect.tsx  # Dropdown to pick collection
│   ├── hooks/
│   │   └── useChat.ts       # Manages conversation state
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
└── tsconfig.json
```

## Core Components

### App.tsx
Main layout with two sections:
- **Sidebar**: collection selector, upload area, list of uploaded resumes
- **Main**: chat interface (messages + input)

### api/client.ts
Typed API wrapper for backend communication:
- `uploadResumes(files, collection)` - upload one or more resumes
- `askQuestion(question, collection)` - ask a question
- `getCollections()` - list available collections
- `clearCollection(collection)` - clear a collection

### hooks/useChat.ts
Manages Q&A conversation state:
- Tracks messages (user questions + assistant answers)
- Handles loading state
- Stores source attributions for each answer

## Tech Stack

- **Vite** - bundler
- **React 18** - UI framework
- **TypeScript** - type safety
- **Tailwind CSS** - styling
- **fetch** - API calls (no axios needed)

## Setup

```bash
npm create vite@latest . -- --template react-ts
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Development

```bash
npm run dev
```

Backend must be running at `http://localhost:8000`.
