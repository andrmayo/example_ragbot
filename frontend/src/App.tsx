import { useState, useEffect } from "react";
import { ChatMessage } from "./components/ChatMessage";
import { ChatInput } from "./components/ChatInput";
import { FileUpload } from "./components/FileUpload";
import { CollectionSelect } from "./components/CollectionSelect";
import { useChat } from "./hooks/useChat";
import {
  uploadResumes,
  getCollections,
  clearCollection,
  clearAll,
  removeResume,
} from "./api/client";

function App() {
  const [collection, setCollection] = useState("default");
  const [collections, setCollections] = useState<string[]>(["default"]);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const [newCollection, setNewCollection] = useState("");
  const [collectionToDelete, setCollectionToDelete] = useState("default");
  const [resumeToDelete, setResumeToDelete] = useState("");

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

  const handleDeleteResume = async () => {
    if (!resumeToDelete) return;
    try {
      await removeResume(collection, resumeToDelete);
      setUploadedFiles((prev) => prev.filter((f) => f !== resumeToDelete));
      setResumeToDelete("");
    } catch (e) {
      console.error("Failed to delete resume:", e);
    }
  };

  const handleCollectionChange = (newCollection: string) => {
    setCollection(newCollection);
    setUploadedFiles([]);
    clearMessages();
  };

  const handleDeleteCollection = async () => {
    if (!collectionToDelete) return;
    try {
      await clearCollection(collectionToDelete);
      const res = await getCollections();
      setCollections(
        res.collections.length > 0 ? res.collections : ["default"],
      );
      if (collection === collectionToDelete) {
        setCollection("default");
        setUploadedFiles([]);
        clearMessages();
      }
    } catch (e) {
      console.error("Failed to delete collection:", e);
    }
  };

  const handleDeleteAll = async () => {
    if (!collectionToDelete) return;
    try {
      await clearAll();
      setCollections(["default"]);
      setCollection("default");
      setUploadedFiles([]);
      clearMessages();
    } catch (e) {
      console.error("Failed to delete all:", e);
    }
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
          {/* Select a collection */}
          <div className="flex gap-2 mt-2">
            <input
              type="text"
              value={newCollection}
              onChange={(e) => setNewCollection(e.target.value)}
              placeholder="New collection name"
              className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded"
            />
            {/* Add a collection */}
            <button
              onClick={() => {
                if (newCollection.trim()) {
                  setCollections((prev) => [...prev, newCollection.trim()]);
                  setCollection(newCollection.trim());
                  setNewCollection("");
                  setUploadedFiles([]);
                  clearMessages();
                }
              }}
              className="px-2 py-1 text-sm bg-gray-200 rounded hover:bg-gray-300"
            >
              Add
            </button>
          </div>
          {/* Delete a collection */}
          <div className="mt-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Delete Collection
            </label>
            <div className="flex gap-2">
              <select
                value={collectionToDelete}
                onChange={(e) => setCollectionToDelete(e.target.value)}
                className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded"
              >
                {collections.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
              <button
                onClick={handleDeleteCollection}
                className="px-2 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
              >
                Delete
              </button>
              <button
                onClick={handleDeleteAll}
                className="px-2 py-1 text-sm bg-rd-100 text-red-700 rounded hover:bg-red-200"
              >
                All
              </button>
            </div>
          </div>
        </div>

        {/*Upload files*/}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Upload Resumes
          </label>
          <FileUpload onUpload={handleUpload} disabled={uploading} />
        </div>

        {/*Delete file*/}
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
            <button
              onClick={async () => {
                try {
                  await clearCollection(collection);
                  setUploadedFiles([]);
                  clearMessages();
                } catch (e) {
                  console.error("Failed to clear resumes:", e);
                }
              }}
              className="px-2 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
            >
              Delete All
            </button>
          </div>
        )}

        {uploadedFiles.length > 0 && (
          <div className="mt-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Delete Resume
            </label>
            <div className="flex gap-2">
              <select
                value={resumeToDelete}
                onChange={(e) => setResumeToDelete(e.target.value)}
                className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded"
              >
                <option value="">Select...</option>
                {uploadedFiles.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
              <button
                onClick={handleDeleteResume}
                disabled={!resumeToDelete}
                className="px-2 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 disabled:opacity-50"
              >
                Delete
              </button>
            </div>
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
