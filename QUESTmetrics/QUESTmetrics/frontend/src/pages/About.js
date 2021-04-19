import React from 'react';
import image from '../about.svg';
const About = () => {
	return (
		<div className="about">
			<h1>About</h1>
			<img src={image} />
			<div>
				<h2>About QUESTmetrics</h2>
				<p>
					This product allows instructors in the QUEST Honors Program to track the
					health of the groups in their classes.
				</p>
				<br />

				<p className="subtext">
					There are 5 different components that create each team metric: individual's
					grades on ELMs, the last time the student has checked the class ELMs page, the
					percentage of late assignments, the group's activity on Slack and the total
					responses from a class distrubuted survey.
				</p>
			</div>
			<a href="http://valerian.cs.umd.edu:8001/" target="_blank">
				Visit Our Advertisement!
			</a>
		</div>
	);
};

export default About;
