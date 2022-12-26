import { css } from "@emotion/css";
import {
  Button,
  Chip,
  Paper,
  TextField,
  Typography,
  Slider,
  OutlinedInput,
  useTheme,
} from "@mui/material";
import { LoadingButton } from "@mui/lab";
import { useState } from "react";
import "./App.css";
import { GENRE_NAMES } from "./constants/GENRE_NAMES";
import useClassifier from "./hooks/useClassifier";
import useGenerator from "./hooks/useGenerator";

function App() {
  const theme = useTheme();
  const [step, setStep] = useState("classify");
  const [lyricsInput, setLyricsInput] = useState("");
  const [genresSelected, setGenresSelected] = useState(
    GENRE_NAMES.reduce((g, acc) => ({ ...acc, [g]: false }), {})
  );

  const { returnedGenres, classify } = useClassifier(setGenresSelected);
  const { generatedLyrics, generate, length, setLength, isLoading } =
    useGenerator();

  return (
    <div className="App">
      <div
        className={css`
          display: flex;
          flex-direction: column;
          align-items: center;
        `}
      >
        <Typography variant="h2" fontWeight={700} marginBottom={4}>
          Lyrics Generator
        </Typography>
        <Paper
          sx={{
            padding: "16px",
            width: "60vw",
            minWidth: "640px",
            display: "flex",
            flexDirection: "column",
            backgroundColor: theme.palette.grey[100],
            alignItems: "center",
          }}
        >
          <div
            className={css`
              margin-top: 8px;
              margin-bottom: 8px;
            `}
          >
            <Typography variant="h5" fontWeight={700}>
              Step 1: Enter Seed Lyrics
            </Typography>
            <Typography variant="caption">
              Input some idea or reference lyrics here.
            </Typography>
          </div>
          <TextField
            fullWidth
            placeholder="Input seed lyrics here..."
            multiline
            rows={6}
            value={lyricsInput}
            onChange={(e) => setLyricsInput(e.target.value)}
            sx={{ marginTop: 1, marginBottom: 2 }}
          />
          <div
            className={css`
              margin-top: 24px;
              margin-bottom: 8px;
            `}
          >
            <Typography variant="h5" fontWeight={700}>
              Step 2: Guess Genres
            </Typography>
            <Typography variant="caption">
              Let the system guess what genre you are probably going for based
              on your seed lyrics.
            </Typography>
          </div>
          <Button
            variant="contained"
            sx={{ marginTop: 2, marginBottom: 2 }}
            onClick={() => classify(lyricsInput)}
          >
            Guess Genres
          </Button>
          <div
            className={css`
              margin-bottom: 4px;
            `}
          >
            {returnedGenres.length !== 0 && (
              <Typography variant="overline">
                Your seed lyrics sounds like
              </Typography>
            )}
          </div>
          <div
            className={css`
              display: flex;
              width: 100%;
              justify-content: center;
              gap: 5px;
              margin-bottom: 28px;
            `}
          >
            {returnedGenres.map((g) => (
              <Chip key={g} label={g} />
            ))}
          </div>
          <div
            className={css`
              margin-top: 36px;
              margin-bottom: 12px;
            `}
          >
            <Typography variant="h5" fontWeight={700}>
              Step 3: Generate Lyrics
            </Typography>
            <Typography variant="caption">
              Generate new lyrics based on seed lyrics and a selected set of
              genres.
            </Typography>
          </div>
          <div
            className={css`
              margin-bottom: 16px;
            `}
          >
            <Typography variant="overline">Seed Lyrics</Typography>
            <Typography variant="body2" fontStyle="italic">
              {lyricsInput.length === 0
                ? "(empty)"
                : `"${lyricsInput.slice(0, 80)}${
                    lyricsInput.length > 80 ? "..." : ""
                  }"`}
            </Typography>
          </div>
          <div
            className={css`
              margin-bottom: 16px;
              max-width: 640px;
            `}
          >
            <Typography variant="overline">Selected genres</Typography>
            <div
              className={css`
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                justify-content: center;
              `}
            >
              {GENRE_NAMES.map((name) => (
                <Chip
                  key={name}
                  clickable
                  label={name}
                  color={genresSelected[name] ? "primary" : "default"}
                  onClick={() =>
                    setGenresSelected((state) => ({
                      ...state,
                      [name]: !state[name],
                    }))
                  }
                />
              ))}
            </div>
          </div>
          <div
            className={css`
              display: flex;
              flex-direction: column;
              flex-wrap: wrap;
              justify-content: center;
              margin-bottom: 12px;
            `}
          >
            <Typography variant="overline">Generate Lyrics Length</Typography>
            <div
              className={css`
                display: flex;
                flex-direction: column;
                flex-wrap: wrap;
                justify-content: center;
                align-items: center;
              `}
            >
              <Slider
                sx={{ width: 160 }}
                size="small"
                defaultValue={100}
                valueLabelDisplay="auto"
                value={length}
                onChange={(_, value) => setLength(value)}
                min={10}
                max={500}
              />
              <Typography>{length}</Typography>
            </div>
          </div>
          <LoadingButton
            loading={isLoading}
            variant="contained"
            sx={{ marginTop: 2, marginBottom: 2 }}
            onClick={() => generate(lyricsInput, genresSelected)}
          >
            Generate Lyrics
          </LoadingButton>
          <TextField
            fullWidth
            placeholder="Results will be shown here..."
            multiline
            rows={16}
            onChange={(e) => setLyricsInput(e.target.value)}
            sx={{ marginTop: 1, marginBottom: 2 }}
            inputProps={{ readOnly: true }}
            value={generatedLyrics}
          />
        </Paper>
      </div>
    </div>
  );
}

export default App;
