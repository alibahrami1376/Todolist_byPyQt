import express from 'express';
import cors from 'cors';
import projects from './routes/projects';
import columns from './routes/columns';
import steps from './routes/steps';
import tags from './routes/tags';
import attachments from './routes/attachments';
import comments from './routes/comments';

const app = express();
app.use(cors());
app.use(express.json());

app.use('/projects', projects);
app.use('/columns', columns);
app.use('/steps', steps);
app.use('/tags', tags);
app.use('/attachments', attachments);
app.use('/comments', comments);

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`API listening on ${port}`));


