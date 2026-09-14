import { useEffect, useState } from "react";
import { getHealth } from "./services/api";


function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [backendData, setBackendData] = useState(null);


  useEffect(() => {
    async function checkBackend() {
      try {
        const data = await getHealth();

        setBackendData(data);
        setBackendStatus("Connected");
      } catch (error) {
        console.error(error);
        setBackendStatus("Disconnected");
      }
    }

    checkBackend();
  }, []);


  return (
    <div className="min-h-screen bg-gray-100">

      <header className="border-b bg-white">
        <div className="mx-auto max-w-7xl px-6 py-5">
          <h1 className="text-2xl font-bold text-gray-900">
            AI Insurance Sampler
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            AI-powered life insurance sampling and risk assessment
          </p>
        </div>
      </header>


      <main className="mx-auto max-w-7xl px-6 py-10">

        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900">
            System Overview
          </h2>

          <p className="mt-2 text-gray-600">
            Batch 1 foundation is successfully running.
          </p>
        </div>


        <div className="grid gap-6 md:grid-cols-3">

          <div className="rounded-xl bg-white p-6 shadow-sm">
            <p className="text-sm font-medium text-gray-500">
              Frontend
            </p>

            <p className="mt-2 text-lg font-semibold text-green-600">
              Running
            </p>
          </div>


          <div className="rounded-xl bg-white p-6 shadow-sm">
            <p className="text-sm font-medium text-gray-500">
              Backend API
            </p>

            <p
              className={`mt-2 text-lg font-semibold ${
                backendStatus === "Connected"
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {backendStatus}
            </p>
          </div>


          <div className="rounded-xl bg-white p-6 shadow-sm">
            <p className="text-sm font-medium text-gray-500">
              Database
            </p>

            <p className="mt-2 text-lg font-semibold text-gray-500">
              Coming in Batch 2
            </p>
          </div>

        </div>


        {backendData && (
          <div className="mt-8 rounded-xl bg-white p-6 shadow-sm">

            <h3 className="text-lg font-semibold text-gray-900">
              Backend Information
            </h3>

            <div className="mt-4 space-y-2 text-sm text-gray-600">
              <p>
                <span className="font-medium">Service:</span>{" "}
                {backendData.service}
              </p>

              <p>
                <span className="font-medium">Version:</span>{" "}
                {backendData.version}
              </p>

              <p>
                <span className="font-medium">Environment:</span>{" "}
                {backendData.environment}
              </p>

              <p>
                <span className="font-medium">Status:</span>{" "}
                {backendData.status}
              </p>
            </div>

          </div>
        )}

      </main>

    </div>
  );
}


export default App;