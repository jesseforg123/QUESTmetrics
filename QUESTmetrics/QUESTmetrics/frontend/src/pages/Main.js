import React from 'react';
import { Switch, Route, NavLink } from 'react-router-dom';

// components
import Home from './Home';
import Classes from './Classes';
import SurveyInstructor from './SurveyInstructor';
import SurveyStudent from './SurveyStudent';
import About from './About';
import Settings from './Settings';

// icons
import { AiFillHome } from 'react-icons/ai';
import { HiUserGroup } from 'react-icons/hi';
import { RiSurveyFill } from 'react-icons/ri';
import { GoSettings } from 'react-icons/go';
import { VscInfo } from 'react-icons/vsc';

// Navbar
const Navbar = () => (
	<div className="navbar">
		<ul className="navbar-nav">
			<li className="nav-item">
				<NavLink exact className="nav-link" to="/">
					<AiFillHome />
					<div className="label">Home</div>
				</NavLink>
			</li>

			<li className="nav-item">
				<NavLink className="nav-link" to="/classes">
					<HiUserGroup />
					<div className="label">Classes</div>
				</NavLink>
			</li>

			<li className="nav-item">
				<NavLink exact className="nav-link" to="/survey-instructor">
					<RiSurveyFill />
					<div className="label">Survey</div>
				</NavLink>
			</li>

			<li className="nav-item">
				<NavLink exact className="nav-link" to="/about">
					<VscInfo />
					<div className="label">About</div>
				</NavLink>
			</li>

			<li className="nav-item">
				<NavLink exact className="nav-link" to="/settings">
					<GoSettings />
					<div className="label">Settings</div>
				</NavLink>
			</li>
		</ul>
	</div>
);

const routes = [
	{ path: '/classes', name: 'Classes', Component: Classes },
	{
		path: '/survey-instructor',
		name: 'Instructor Survey',
		Component: SurveyInstructor,
	},
	{ path: '/about', name: 'About', Component: About },
	{ path: '/settings', name: 'Settings', Component: Settings },
	{ path: '/', name: 'Home', Component: Home },
];

export default function Main(props) {
	const page = props => {
		if (props.privilege == 2) {
			return <SurveyStudent token={props.token} />;
		}
		if (props.privilege == 0) return <div></div>;
		if (props.privilege == 1) {
			return (
				<div className="dashboard">
					<Route path="/">
						<Navbar />
						<div className="main">
							<Switch>
								{routes.map(({ path, Component }, key) => (
									<Route path={path} key={key}>
										<Component />
									</Route>
								))}
							</Switch>
						</div>
					</Route>
				</div>
			);
		}
	};

	return <div>{page(props)}</div>;
}
