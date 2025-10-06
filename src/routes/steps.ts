import { Router } from 'express';
import { prisma } from '../prisma';
const r = Router();

r.post('/columns/:id/steps', async (req, res) => {
  const { id } = req.params;
  const { projectId, title, description, ...rest } = req.body;
  const step = await prisma.projectStep.create({
    data: { columnId: id, projectId, title, description, ...rest },
  });
  res.json(step);
});

r.patch('/:id', async (req, res) => {
  const { id } = req.params;
  const step = await prisma.projectStep.update({ where: { id }, data: req.body });
  res.json(step);
});

r.delete('/:id', async (req, res) => {
  const { id } = req.params;
  await prisma.projectStep.delete({ where: { id } });
  res.status(204).end();
});

r.patch('/:id/move', async (req, res) => {
  const { id } = req.params;
  const { columnId } = req.body;
  const step = await prisma.projectStep.update({ where: { id }, data: { columnId } });
  res.json(step);
});

export default r;


