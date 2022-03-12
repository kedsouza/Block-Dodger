const ScoreCard = ({username, score}) => {

    return (
        <div className='w3-display-bottommiddle w3-container w3-lime w3-padding'style={{height:"100px", width:"400px"}} >            
            <h4>UserName: {username}</h4>
            <h4>Score: {score}</h4>

        </div>
       
    )
}

ScoreCard.defaultProps = {
    username: "",
    score: 0
}
export default ScoreCard