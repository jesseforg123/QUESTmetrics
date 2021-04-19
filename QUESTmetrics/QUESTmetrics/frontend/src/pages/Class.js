import React, { useState, useEffect } from 'react';
import { NavLink, Route, useParams, useRouteMatch } from 'react-router-dom';
import Collapsible from 'react-collapsible';
import Group from './Group';
import { fetchAllGroups, fetchGroupsInClass } from '../utils/fetch';
import { pink } from '@material-ui/core/colors';

const Class = () => {
	const [groupsInClass, setGroups] = useState({});
	const [active, setActive] = useState(null);
	const { classID } = useParams();
	const { url } = useRouteMatch();
	const [expanded, setExpanded] = useState(false);

	const [nameOfClass, setNameOfClass] = useState('');

	useEffect(() => {
		(async () => {
			if (classID === 'all') await fetchAllGroups().then(data => setGroups(data));
			else await fetchGroupsInClass(classID).then(data => setGroups(data));
		})();
		setActive(null);
		setNameOfClass(classID.toString().toUpperCase());
	}, [url, classID]);

	function collapse() {
		if (document.querySelector('.info').style.visibility == 'hidden') {
			setNameOfClass(classID.toString().toUpperCase());
			document.querySelector('.info').style.height = 'auto';
			document.querySelector('.info').style.visibility = 'visible';
			document.querySelector('.info').style.overflow = 'visible';
			document.querySelector('.info').style.opacity = '1';
			document.querySelector('.info').style.transition = 'all 1.5s ease';
			document.getElementById('title').innerHTML =
				"<div style='display: flex; align-items: center;'>" +
				// `${nameOfClass}`;
				'<span style="font-size: 1.5rem; margin: 0rem 0.5rem; font-weight: 400; ">(Click to collapse)</span>' +
				'</div>';
			document.getElementById('title').style.marginBottom = '2rem';
			document.getElementById('title').style.fontWeight = '700';
		} else {
			document.querySelector('.info').style.visibility = 'hidden';
			document.querySelector('.info').style.height = '0rem';
			document.querySelector('.info').style.overflow = 'hidden';
			document.querySelector('.info').style.opacity = '0';
			document.querySelector('.info').style.transition = 'all 1.5s ease';
			document.getElementById('title').innerHTML =
				'Click <span style="color:indianred; font-weight: bold; letter-spacing: 0.05rem">Here</span> to Open Class Details';
			document.getElementById('title').style.marginBottom = '0rem';
			document.getElementById('title').style.fontWeight = '400';
		}
	}

	const groupsInClassData = Object.keys(groupsInClass).map(g => {
		const { groupId, name, className, watch, groupHealth } = groupsInClass[g];
		let cssClass = active === groupId ? 'groupInClass active' : 'groupInClass';

		switch (groupHealth) {
			case 1:
				cssClass += ' red';
				break;
			case 2:
				cssClass += ' yellow';
				break;
			case 3:
				cssClass += ' green';
				break;
			default:
				cssClass += '';
		}

		return (
			<NavLink
				onClick={() => {
					setActive(groupId);
					collapse();
				}}
				className={cssClass}
				key={groupId}
				to={`${url}/${name}`}>
				{name}
			</NavLink>
		);
	});

	// console.log(document.getElementsByClassName('class-iframe')[0]);
	return (
		<div>
			<h2 id="title" onClick={() => collapse()}>
				<div style={{ display: 'flex', alignItems: 'center' }}>
					{/* {nameOfClass} */}
					<span
						style={{ fontSize: '1.5rem', margin: '0rem 0.5rem', fontWeight: '400' }}>
						(Click to collapse)
					</span>
				</div>
			</h2>
			<div className="info">
				<Collapsible trigger="Visualizations">
					<div className="vis">
						{
							<iframe
								className="class-iframe"
								title={classID}
								width="97%"
								height="700"
								border="none"
								frameBorder="0"
								scrolling="yes"
								src={
									classID !== 'all'
										? `http://valerian.cs.umd.edu:8080/superset/dashboard/${classID}`
										: `http://valerian.cs.umd.edu:8080/superset/dashboard/classes`
								}></iframe>
						}
					</div>
				</Collapsible>
				<Collapsible trigger="Groups">
					<div className="classAllGroups">
						<div className="groupsInClass"> {groupsInClassData} </div>
					</div>
				</Collapsible>
			</div>
			<hr />
			<Route exact path={`${url}/:groupname`}>
				<Group />
			</Route>
		</div>
	);
};

export default Class;
