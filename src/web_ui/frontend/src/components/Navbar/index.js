// Filename - "./components/Navbar.js

import { Nav, NavLink, NavMenu } from "./NavbarElements";

const Navbar = () => {
    return (
        <>
            <Nav>
                <NavMenu>
                    <NavLink to="/about">
                        About
                    </NavLink>
                    <NavLink to="/navigator">
                        Navigator
                    </NavLink>
                </NavMenu>
            </Nav>
        </>
    );
};

export default Navbar;
