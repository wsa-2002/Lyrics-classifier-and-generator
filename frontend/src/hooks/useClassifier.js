import { useState } from "react";

import { agent } from "../agent";
import { GENRE_NAMES } from "../constants/GENRE_NAMES";

const useClassifier = (setGenresSelected) => {
  const [returnedGenres, setReturnedGenres] = useState([]);
  const classify = async (seed) => {
    const res = await agent.get("/genres-classify", {
      params: { lyrics: seed, lyrics_length: seed.length + 100 },
    });
    setReturnedGenres(res.data);
    setGenresSelected(
      GENRE_NAMES.reduce(
        (acc, g) => ({ ...acc, [g]: res.data.includes(g) }),
        {}
      )
    );
  };

  return { returnedGenres, classify };
};

export default useClassifier;
