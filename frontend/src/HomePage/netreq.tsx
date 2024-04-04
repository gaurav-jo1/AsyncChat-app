import React, { FormEvent, useState, useEffect } from "react";
type Language = {
  id: string;
  language_name: string;
};
const App: React.FC = () => {
  const [language, setLanguage] = useState<string>("");
  const [makeRequest, setMakeRequest] = useState<boolean>(false);
  const [languageList, setLanguageList] = useState<Language[]>([]);

  useEffect(() => {
    const fetch_data = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/");

        if (!response.ok) {
          console.log("Network request failed.");
        }

        const result = await response.json();
        console.log(result);
        setLanguageList(result.languages);
        setLanguage("")
        setMakeRequest(false)
      } catch (error) {
        console.log(error);
      }
    };

    fetch_data();
  }, [makeRequest]);

  const post_data = async (e: FormEvent) => {
    e.preventDefault();

    const form_data = {
      language: language,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form_data),
      });

      const result = await response.json();
      console.log("Success: ", result);
      setMakeRequest(true);
    } catch (error) {
      console.log("Error: ", error);
    }
  };
  return (
    <div>
      <h1>Data</h1>
      <form onSubmit={post_data}>
        <input
          type="text"
          name=""
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          placeholder="Enter the language"
        />
        <button type="submit">Submit</button>
      </form>

      <h1>Languages List</h1>
      <div>
        {languageList && (
          <ul>
            {languageList.map((name) => (
              <li key={name.id}>{name.language_name}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default App;
