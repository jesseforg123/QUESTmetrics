import React, {  lazy, Suspense, Spinner, useState, useEffect } from 'react';
import { NavLink, Route, useRouteMatch } from 'react-router-dom';

import Class from './Class';
import { fetchAllClasses } from '../utils/fetch';


const Classes = () => {
	const [classes, setClasses] = useState({});
	const [active, setActive] = useState('all');
	const { url } = useRouteMatch();
	const [loaded, setLoaded] = useState(false);


	useEffect(() => {
		(async () => await fetchAllClasses().then(data => {setClasses(data); setLoaded(true);}))();
		setActive('all');
	}, [url]);

	var classesData = Object.keys(classes).map(c => {
		const name = classes[c].className.toString();
		const className = active === name ? 'class active-class' : 'class';
		return (
			<NavLink
				onClick={() => setActive(name)}
				className={className}
				key={name}
				to={`${url}/${name}`}>
				{name}
			</NavLink>
		);
	});

	return (
		<div>
			<h1>Classes</h1>

			<Route exact path={url}>
				<div className="classes">
					{loaded && (<NavLink className="class" to={`${url}/all`}>
						All
					</NavLink>)}
						{classesData}
				</div>
			</Route>

			<Route path={`${url}/:classID`}>
				<div className="classes">
					<NavLink
						onClick={() => setActive('all')}
						className={active === 'all' ? 'class active-class' : 'class'}
						to={`${url}/all`}>
						All
					</NavLink>
					{classesData}
				</div>
				<hr />
				<Class />
			</Route>
		</div>
	);
};

export default Classes;
