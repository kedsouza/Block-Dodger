import Header from "./components/Header"
import Game from "./components/Game"
import ScoreCard from "./components/ScoreCard"
import HighScoresTable from "./components/HighScoresTable"

function App() {
  return (
    <div className="w3-container">
      <Header/>
      <Game/>
      <HighScoresTable/>
      <ScoreCard/>
    </div>
  );
}

export default App;
