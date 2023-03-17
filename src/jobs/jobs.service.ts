import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import mongoose from 'mongoose';
import { CreateJobDto } from './dto/create-job.dto';
import { UpdateJobDto } from './dto/update-job.dto';
import { Job } from './schemas/job.schema';

@Injectable()
export class JobsService {
  constructor(
    @InjectModel(Job.name)
    private jobModel: mongoose.Model<Job>,
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

  async findAll(): Promise<Job[]> {
    return await this.jobModel.find();
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
