import { useState } from "react";

import { agent } from "../agent";
import { GENRE_NAMES } from "../constants/GENRE_NAMES";

const useGenerator = () => {
  const [loading, setLoading] = useState(false);
  const [generatedLyrics, setGeneratedLyrics] = useState("");
  const [length, setLength] = useState(100);
  const generate = async (seed, genresSelected) => {
    const genres = GENRE_NAMES.filter((name) => genresSelected[name]);
    setLoading(true);
    const res = await agent.post("lyrics-generate", genres, {
      params: { lyrics: seed, lyrics_length: length },
    });
    setGeneratedLyrics(res.data);
    setLoading(false);
  };

  return { generatedLyrics, generate, length, setLength, isLoading: loading };
};

export default useGenerator;
