import { useState, useEffect } from "react";
import { ChatMessage } from "./components/ChatMessage";
import { ChatInput } from "./components/ChatInput";
import { FileUpload } from "./components/FileUpload";
import { CollectionSelect } from "./components/CollectionSelect";
import { useChat } from "./hooks/useChat";
import { uploadResumes, getCollections } from "./api/client";

function App() {
  const [collection, setCollection] = useState("default");
  const [collections, setCollections] = useState<string[]>(["default"]);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);

  const { messages, loading, error, ask, clearMessages } = useChat(collection);

  // Fetch collections on mount
  useEffect(() => {
    getCollections()
      .then((res) => {
        if (res.collections.length > 0) {
          setCollections(res.collections);
        }
      })
      .catch(console.error);
  }, []);

  const handleUpload = async (files: File[]) => {
    setUploading(true);
    try {
      await uploadResumes(files, collection);
      setUploadedFiles((prev) => [...prev, ...files.map((f) => f.name)]);
      // Refresh collections in case this created a new one
      const res = await getCollections();
      if (res.collections.length > 0) {
        setCollections(res.collections);
      }
    } catch (e) {
      console.error("Upload failed:", e);
    } finally {
      setUploading(false);
    }
  };

  const handleCollectionChange = (newCollection: string) => {
    setCollection(newCollection);
    setUploadedFiles([]);
    clearMessages();
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 p-4 flex flex-col gap-4">
        <h1 className="text-xl font-bold text-gray-800">Resume RAGBot</h1>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Collection
          </label>
          <CollectionSelect
            collections={collections}
            selected={collection}
            onSelect={handleCollectionChange}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Upload Resumes
          </label>
          <FileUpload onUpload={handleUpload} disabled={uploading} />
        </div>

        {uploadedFiles.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Uploaded ({uploadedFiles.length})
            </label>
            <ul className="text-sm text-gray-600 space-y-1">
              {uploadedFiles.map((name) => (
                <li key={name} className="truncate">
                  {name}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <p className="text-center text-gray-400 mt-8">
              Upload resumes and ask questions about them
            </p>
          ) : (
            messages.map((msg, i) => (
              <ChatMessage
                key={i}
                role={msg.role}
                content={msg.content}
                sources={msg.sources}
              />
            ))
          )}
          {loading && <p className="text-gray-400 italic">Thinking...</p>}
          {error && <p className="text-red-500">{error}</p>}
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <ChatInput onSubmit={ask} disabled={loading} />
        </div>
      </div>
    </div>
  );
}

export default App;
