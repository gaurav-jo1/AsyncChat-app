import React, { useState } from "react";
import axios from "axios";

interface language_list {
  id: string;
  language_name: string;
}

const App: React.FC = () => {
  const [data, setData] = useState<language_list[]>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = () => {
    axios
      .get("http://127.0.0.1:8000/api/")
      .then((response) => {
        // Assuming the response.data contains the data you need
        setData(response.data.languages);
      })
      .catch((error) => {
        setError(error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  // const fetchA_Data = async () => {
  //   try {
  //     const response = await fetch("http://127.0.0.1:8000/api/");

  //     if (!response.ok) {
  //       throw new Error("Network request failed");
  //     }

  //     const result = await response.json();
  //     console.log(result);
  //   } catch (error) {
  //     console.log(error);
  //   } finally {
  //     console.log(false);
  //   }
  // };

  return (
    <div>
      <h1>Hello World</h1>

      <div>
        <button onClick={() => fetchData()}> Get List of Languages</button>
      </div>

      {data && data.map((item) => (
        <div key={item.id}>
          <p>{item.language_name}</p>
        </div>
      ))}
    </div>
  );
};

export default App;
