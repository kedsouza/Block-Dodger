const Header = ({title}) => {

    return (
        <header className='w3-display-container w3-display-topmiddle'>
            <h1 class="w3-xxxlarge">{title}</h1>
        </header>
    )
}

Header.defaultProps = {
    title: 'Block Dodger',
}

export default Header