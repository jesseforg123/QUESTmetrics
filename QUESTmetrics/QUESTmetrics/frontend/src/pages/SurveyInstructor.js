import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

import { postSurvey } from '../utils/fetch';

function SurveyInstructor() {
	const [questions, setQuestions] = useState([]);
	const [surveyClass, setSurveyClass] = useState(null);
	let history = useHistory();

	const [saved, setSaved] = useState(false);
	const [classSelected, setClassSelected] = useState(false);

	const handleQuestionInput = (index, e) => {
		const allQuestions = [...questions];
		allQuestions[index]['question'] = e.target.value;
		setQuestions(allQuestions);
	};

	const handleSave = async e => {
		if (classSelected) {
			let empty = false;
			for (let i = 0; i < questions.length; i++) {
				console.log(questions[i]['question']);
				if (questions[i]['question'].trim() === '') empty = true;
			}
			if (!empty) {
				await postSurvey(questions, surveyClass.toString().toUpperCase());
				history.push('/');
			}
		}
	};

	const handleAdd = () => {
		setQuestions([...questions, { question: '' }]);
	};

	const handleRemove = index => {
		const allQuestions = [...questions];
		allQuestions.splice(index, 1);
		setQuestions(allQuestions);
	};

	const handleSelectClass = e => {
		setClassSelected(true);
		setSurveyClass(e.target.value);
	};

	const selectClass = (
		<div className="selectclass" onChange={e => handleSelectClass(e)}>
			<div>
				<input type="radio" value="All" name="class" /> All
			</div>
			<div>
				<input type="radio" value="BMGT390H" name="class" /> BMGT390H
			</div>
			<div>
				<input type="radio" value="BMGT438A" name="class" /> BMGT438A
			</div>
			<div>
				<input type="radio" value="BMGT490H" name="class" /> BMGT490H
			</div>
		</div>
	);

	return (
		<div className="survey-instructor">
			<h1>Survey</h1>
			<div className="container">
				{questions.length == 0 ? (
					<div>
						<div className="add-button-text" onClick={handleAdd}>
							Create New Survey
						</div>
						<br />
						<br />

						<iframe
							className="class-iframe"
							title="test"
							width="97%"
							height="700"
							border="none"
							frameBorder="0"
							scrolling="yes"
							src="http://valerian.cs.umd.edu:8080/superset/dashboard/surveyresponses"></iframe>
					</div>
				) : (
					<div>
						{!classSelected ? (
							<div className="warning warningClass">Please select a class.</div>
						) : (
							<div></div>
						)}
						{selectClass}
						<form onSubmit={handleSave}>
							{questions.map((Question, index) => (
								<div key={index} className="question">
									<div className="question-number">{index + 1}: </div>
									<input
										autoComplete="off"
										type="text"
										name="question"
										className="question-input"
										value={Question.question}
										onChange={e => handleQuestionInput(index, e)}
										placeholder={
											index == 0 ? 'There is enough time to complete homework.' : ''
										}
									/>

									<div className="remove-button" onClick={() => handleRemove(index)}>
										-
									</div>
								</div>
							))}
						</form>
						<div className="add-button" onClick={handleAdd}>
							+
						</div>
						<div className="save-button" onClick={handleSave}>
							Clear Existing Responses and Send New Survey
						</div>
						{!saved ? (
							<div className="warning">
								Warning: your questions will not be saved until you press the button
								above
							</div>
						) : (
							<div></div>
						)}
					</div>
				)}
			</div>
			<p>
				In this page, you can create a new survey for the students to take.
				<br />
				<span className="subtext">
					The students will answer each of your questions according to the{' '}
					<em>Likert scale</em>, specifically with the following five options — <br />
					<em>Strongly Disagree, Disagree, Neutral, Agree, and Strongly Agree.</em>
				</span>
				<br />
				<br />
				<span className="please">
					Note: If any of the classes you have chosen already have a current survey, it
					will be erased and replaced with this one.
				</span>
			</p>
		</div>
	);
}

export default SurveyInstructor;
