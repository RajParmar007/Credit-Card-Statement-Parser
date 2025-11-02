// app/page.js

"use client"; // This must be at the top to use hooks

import { useState } from "react";

export default function Home() {
  const [bank, setBank] = useState("hdfc"); // Default selected bank
  const [file, setFile] = useState(null);
  const [output, setOutput] = useState(null); // Will store our JSON
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !bank) {
      setError("Please select a bank and a file.");
      return;
    }

    setLoading(true);
    setOutput(null);
    setError(null);

    const formData = new FormData();
    formData.append("bank", bank);
    formData.append("file", file);

    try {
      // Send the data to our Python API
      const response = await fetch("http://localhost:5001/parse", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle errors from the API
        throw new Error(data.error || "Something went wrong");
      }

      // Success! Store the JSON data to display it
      setOutput(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-12 bg-gray-50">
      <h1 className="text-4xl font-bold mb-8 text-gray-800">
        Credit Card Statement Parser
      </h1>

      <form
        onSubmit={handleSubmit}
        className="w-full max-w-lg p-8 bg-white rounded-lg shadow-md"
      >
        <div className="mb-6">
          <label
            htmlFor="bank"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            1. Select Bank
          </label>
          <select
            id="bank"
            value={bank}
            onChange={(e) => setBank(e.target.value)}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
          >
            <option value="hdfc">HDFC Bank</option>
            <option value="idfc">IDFC First Bank</option>
            <option value="axis">Axis Bank</option>
            <option value="icici">ICICI Bank</option>
          </select>
        </div>

        <div className="mb-6">
          <label
            htmlFor="file"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            2. Upload PDF Statement
          </label>
          <input
            type="file"
            id="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center disabled:bg-gray-400"
        >
          {loading ? "Parsing..." : "Parse Statement"}
        </button>
      </form>

      {/* --- This is where the output appears --- */}

      {error && (
        <div className="w-full max-w-lg mt-6 p-4 bg-red-100 text-red-700 border border-red-300 rounded-lg">
          <strong>Error:</strong> {error}
        </div>
      )}

      {output && (
        <div className="w-full max-w-4xl mt-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">
            Parsed Data
          </h2>
          <pre className="p-6 bg-gray-900 text-white rounded-lg text-sm overflow-x-auto">
            {JSON.stringify(output, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}