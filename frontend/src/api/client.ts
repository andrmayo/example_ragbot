const API_BASE = "http://localhost:8000";

export interface AnswerResponse {
  answer: string;
  sources: string[];
}

export interface UploadResponse {
  message: string;
}

export interface BatchUploadResponse {
  message: string;
  files: Record<string, string>;
}

export interface CollectionsResponse {
  collections: string[];
}

export async function uploadResume(
  file: File,
  collection: string = "default",
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE}/upload?collection=${encodeURIComponent(collection)}`,
    { method: "POST", body: formData },
  );

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }

  return response.json();
}

export async function uploadResumes(
  files: File[],
  collection: string = "default",
): Promise<BatchUploadResponse> {
  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }

  const response = await fetch(
    `${API_BASE}/upload_batch?collection=${encodeURIComponent(collection)}`,
    { method: "POST", body: formData },
  );

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }

  return response.json();
}

export async function askQuestion(
  question: string,
  collection: string = "default",
): Promise<AnswerResponse> {
  const response = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, collection }),
  });

  if (!response.ok) {
    throw new Error(`Ask failed: ${response.statusText}`);
  }

  return response.json();
}

export async function getCollections(): Promise<CollectionsResponse> {
  const response = await fetch(`${API_BASE}/collections`);

  if (!response.ok) {
    throw new Error(`Failed to get collections: ${response.statusText}`);
  }

  return response.json();
}

export async function clearCollection(collection: string): Promise<void> {
  const response = await fetch(
    `${API_BASE}/clear/${encodeURIComponent(collection)}`,
    { method: "DELETE" },
  );

  if (!response.ok) {
    throw new Error(`Failed to clear collection: ${response.statusText}`);
  }
}

export async function clearAll(): Promise<void> {
  const response = await fetch(`${API_BASE}/clear_all`, { method: "DELETE" });

  if (!response.ok) {
    throw new Error(`Failed to clear all: ${response.statusText}`);
  }
}

export async function removeResume(
  collection: string,
  filename: string,
): Promise<void> {
  const response = await fetch(
    `${API_BASE}/resume/${encodeURIComponent(collection)}/${encodeURIComponent(filename)}`,
    { method: "DELETE" },
  );

  if (!response.ok) {
    throw new Error(`Failed to remove resume: ${response.statusText}`);
  }
}
