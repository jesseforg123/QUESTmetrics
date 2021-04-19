import React, { useState, useEffect } from 'react';
import { NavLink, Route, useRouteMatch } from 'react-router-dom';

import { fetchRedGroups, fetchWatchedGroups, fetchSurvey } from '../utils/fetch';

const Home = () => {
	const [redGroups, setRedGroups] = useState({});
	const [watchedGroups, setWatchedGroups] = useState({});
	const [questions, setQuestions] = useState([]);
	const [students, setStudents] = useState([]);
	const { url } = useRouteMatch();

	useEffect(() => {
		(async () => {
			await fetchRedGroups().then(data => setRedGroups(data));
			await fetchWatchedGroups().then(data => setWatchedGroups(data));
			// await fetchSurvey().then(data => {
			// 	const { questions, students } = data;
			// 	setQuestions(questions);
			// 	setStudents(students);
			// });
		})();
	}, [url]);

	const redGroupsData = Object.keys(redGroups).map(g => {
		const { groupId, name, className, watch, groupHealth } = redGroups[g];
		if (watch === 0)
			return (
				<NavLink className="redGroup" key={groupId} to={`/classes/all/${name}`}>
					{name}
				</NavLink>
			);
		else return null;
	});

	const watchedGroupsData = Object.keys(watchedGroups).map(g => {
		const { groupId, name, className, watch, groupHealth } = watchedGroups[g];
		let cssClass = 'watchedGroup';
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
			<NavLink className={cssClass} key={groupId} to={`/classes/all/${name}`}>
				{name}
			</NavLink>
		);
	});

	const key = questions.map((q, index) => (
		<div className="key-home">
			<div className="key">
				{' '}
				Q{index + 1}: {q}{' '}
			</div>
		</div>
	));
	const questionNumbersMap = questions.map((q, index) => (
		<div className="question-home">Q{index + 1}</div>
	));
	const studentsMap = students.map(s => (
		<div className="studentobj">
			<div className="studentname">
				{s['lastName']}, {s['firstName']}
			</div>
			<div className="studentanswers">
				{s['answers'].map(a => (
					<div className="studentanswer"> {a} </div>
				))}
			</div>
		</div>
	));

	var redGroupsNotWatched = 0;
	redGroupsData.map(g =>
		g != null ? redGroupsNotWatched++ : (redGroupsNotWatched += 0)
	);

	return (
		<div className="home">
			<Route exact path={url}>
				<h1>Home</h1>
				<div className="red">
					{redGroupsNotWatched === 0 ? (
						<div></div>
					) : (
						<div>
							<h2>Red Groups</h2>
							<div className="redGroups"> {redGroupsData} </div>
						</div>
					)}
				</div>
				<div className="watched">
					<h2>Watchlist</h2>
					<div className="watchedGroups"> {watchedGroupsData} </div>
				</div>
				{/* <hr className="hr" />
				<h2 className="results">Survey Results</h2>
				<div className="survey-results">
					<h4>Key</h4>
					{key}
					<div className="questionobj">
						<div className="question-title">Results</div>
						<div className="questions-home"> {questionNumbersMap} </div>
					</div>
					<hr />
					<div className="answers-home"> {studentsMap} </div>
				</div> */}
			</Route>
		</div>
	);
};

export default Home;
