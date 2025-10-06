import { Router } from 'express';
import { prisma } from '../prisma';
const r = Router();

r.post('/steps/:id/comments', async (req, res) => {
  const { id } = req.params;
  const { author, content } = req.body;
  const c = await prisma.comment.create({ data: { stepId: id, author, content } });
  res.json(c);
});

r.get('/steps/:id/comments', async (req, res) => {
  const { id } = req.params;
  res.json(await prisma.comment.findMany({ where: { stepId: id }, orderBy: { createdAt: 'desc' } }));
});

r.delete('/comments/:id', async (req, res) => {
  const { id } = req.params;
  await prisma.comment.delete({ where: { id } });
  res.status(204).end();
});

export default r;


