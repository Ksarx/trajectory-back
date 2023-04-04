import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import mongoose from 'mongoose';
import { DirectionsService } from 'src/directions/directions.service';
import { CreateJobDto } from './dto/create-job.dto';
import { UpdateJobDto } from './dto/update-job.dto';
import { Job } from './schemas/job.schema';

@Injectable()
export class JobsService {
  constructor(
    @InjectModel(Job.name)
    private jobModel: mongoose.Model<Job>,
    private readonly directionService: DirectionsService,
  ) {}

  async create(createJobDto: CreateJobDto): Promise<Job> {
    const count = await this.jobModel.count();
    const newJob: Job = {
      id: count + 1,
      ...createJobDto,
    };
    const res = await this.jobModel.create(newJob);
    return res;
  }

  async findAll(skills?: string, faculty?: string, limit = 5): Promise<Job[]> {
    // Cpp-Python-Создание+сайтов-Философия-Java
    let ids;
    if (faculty) {
      const res = await this.directionService.findAll(faculty);
      ids = new Set();
      res.forEach((item) => {
        const idJobs = item.idJobs;
        for (let i = 0; i < idJobs.length; i++) {
          ids.add(idJobs[i]);
        }
      });
    }

    const findQuery = {
      ...(skills && { skills: { $all: skills.replace('+', ' ').replace('Cpp', 'C++').split('-'); } }),
      ...(ids && { id: { $in: Array.from(ids) } }),
    };
    return await this.jobModel.find(findQuery).limit(limit);
  }

  async findOne(id: number): Promise<Job> {
    const job = await this.jobModel.findOne({ id });

    if (!job) {
      throw new NotFoundException('Job not found.');
    }

    return job;
  }

  async update(jobId: number, updateJobDto: UpdateJobDto): Promise<Job> {
    return await this.jobModel.findOneAndUpdate({ jobId }, updateJobDto, {
      new: true,
      runValidators: true,
    });
  }

  async remove(jobId: number): Promise<Job> {
    return await this.jobModel.findOneAndDelete({ jobId });
  }
}
