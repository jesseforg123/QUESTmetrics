import React, { useState, useEffect } from 'react';

import {
	fetchSurvey,
	postSurveyStudentAnswers,
	getClassesofStudent,
} from '../utils/fetch';

function SurveyStudent(props) {
	const [answers, setAnswers] = useState({});

	const [selectedClass, setSelectedClass] = useState('');
	const [classes, setClasses] = useState([]);
	const [questions, setQuestions] = useState([]);

	const [responded, setResponded] = useState({});

	useEffect(() => {
		(async () => {
			let data = await getClassesofStudent();
			let qs = [],
				cs = [];
			await data.forEach(async c => {
				const classname = c['className'];
				const questionObjects = await fetchSurvey(classname);
				qs = [...qs, ...questionObjects];
				cs = [...cs, classname];
				setQuestions(qs);
				setClasses(cs);
			});
		})();
	}, []);

	const handleSave = e => {
		e.preventDefault();
		console.log(answers, 'here are answers');
		postSurveyStudentAnswers(selectedClass, answers[selectedClass], props.token);

		let newResponded = responded;
		newResponded[selectedClass] = true;
		setResponded(newResponded);
		console.log(responded);
	};

	const handleAnswer = (e, index) => {
		const allAnswers = answers;
		allAnswers[selectedClass][index] = { answer: e.target.value };
		setAnswers(allAnswers);
	};

	const handleClassID = e => {
		const select = e.target.value;
		setSelectedClass(select);
		let newAnswers = answers;
		newAnswers[select] = [];
		setAnswers(newAnswers);
		console.log('setting answers to empty');
	};

	//TODO: IF STUDENT DOESNT SELECT NEW ANSWER IN A NEW CLASS, IT DOESNT WORK

	const surveyQuestions = classname => {
		let index = -1;
		let q = questions.map(q => {
			if (q['className'] == classname) {
				let question = q['question'];
				index++;
				return (
					<div key={index} className="question-student">
						<div>
							<div className="question-number-student">{index + 1}: </div>
							<div className="question-text">{question}</div>
						</div>
						<div className="likert" onChange={e => handleAnswer(e, index)}>
							<div>
								<input className="answer" type="radio" name={index} value="1" />{' '}
								Strongly Disagree
							</div>
							<div>
								<input className="answer" type="radio" name={index} value="2" />{' '}
								Disagree
							</div>
							<div>
								<input className="answer" type="radio" name={index} value="3" /> Neutral
							</div>
							<div>
								<input className="answer" type="radio" name={index} value="4" /> Agree
							</div>
							<div>
								<input className="answer" type="radio" name={index} value="5" />{' '}
								Strongly Agree
							</div>
						</div>
					</div>
				);
			}
		});
		return q;
	};

	return (
		<div className="container-student">
			<h1>Survey</h1>
			<form onSubmit={handleSave}>
				<div className="general">
					<div className="title">Class: </div>
					<select name="classid" className="classid" onChange={e => handleClassID(e)}>
						<option value="none">Select A Class...</option>
						{classes.map(c => (
							<option value={c}>{c}</option>
						))}
					</select>
				</div>
				<br />
				{surveyQuestions(selectedClass)}
			</form>
			<div className="save-button" onClick={handleSave}>
				Save
			</div>
			{responded[selectedClass] ? (
				<div>You have submitted this survey.</div>
			) : (
				<div></div>
			)}
		</div>
	);
}

export default SurveyStudent;
