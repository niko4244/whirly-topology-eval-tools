export async function uploadCircuitImage(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/process-diagram", {
    method: "POST",
    body: form
  });
  if (!res.ok) throw new Error("Upload failed");
  return await res.json();
}