export async function getStatus() {
  // Troque a URL abaixo pelo link gerado pelo Render após o deploy!
  // Exemplo: const response = await fetch("https://onussync-api.onrender.com/status");
  
  const response = await fetch("http://localhost:8000/status"); // <-- Mude aqui depois

  if (!response.ok) {
    throw new Error("Erro ao buscar dados");
  }

  return response.json();
}