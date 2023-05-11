import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import mongoose from 'mongoose';
import { CreateDirectionDto } from './dto/create-direction.dto';
import { UpdateDirectionDto } from './dto/update-direction.dto';
import { Direction } from './schemas/direction.schema';

@Injectable()
export class DirectionsService {
  constructor(
    @InjectModel(Direction.name)
    private directionModel: mongoose.Model<Direction>,
  ) {}

  async create(createDirectionDto: CreateDirectionDto): Promise<Direction> {
    const count = await this.directionModel.count();
    const newDirection: Direction = {
      id: count + 1,
      ...createDirectionDto,
    };
    const res = await this.directionModel.create(newDirection);
    return res;
  }

  async getDirections(
    idJob: number,
    faculty: string,
    page = 1,
    limit = 6,
  ): Promise<any> {
    let query;
    if (faculty) {
      query = faculty.split('-');
    }
    const skip = (page - 1) * limit;
    const totalDocs = await this.directionModel.countDocuments(
      query ? { faculty: query, idJobs: idJob } : { idJobs: idJob },
    );
    const totalPages = Math.ceil(totalDocs / limit);
    const hasNextPage = page < totalPages;
    const hasPrevPage = page > 1;
    const nextPage = hasNextPage ? page + 1 : null;
    const prevPage = hasPrevPage ? page - 1 : null;
    const docs = await this.directionModel
      .find(query ? { faculty: query, idJobs: idJob } : { idJobs: idJob })
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .exec();
    return {
      items: docs,
      meta: {
        totalDocs,
        limit,
        page,
        totalPages,
        hasNextPage,
        hasPrevPage,
        nextPage,
        prevPage,
      },
    };
  }

  async getAllDirections(idJob: number): Promise<any> {
    return await this.directionModel.find({ idJobs: idJob });
  }

  // async findAll(faculty?: string): Promise<Direction[]> {
  //   if (faculty) {
  //     const search = faculty.replace('+', ' ').split('-');
  //     return await this.directionModel.find({ faculty: { $all: search } });
  //   }

  //   return await this.directionModel.find();
  // }

  async findOne(id: number): Promise<Direction> {
    const direction = await this.directionModel.findOne({ id });

    if (!direction) {
      throw new NotFoundException('Direction not found.');
    }

    return direction;
  }

  // async findJobDirections(idJob: number): Promise<Direction[]> {
  //   const directions = await this.directionModel.find({ idJobs: idJob });

  //   if (!directions) {
  //     throw new NotFoundException('Directions not found.');
  //   }

  //   return directions;
  // }

  async update(
    directionId: number,
    updateDirectionDto: UpdateDirectionDto,
  ): Promise<Direction> {
    return await this.directionModel.findOneAndUpdate(
      { directionId },
      updateDirectionDto,
      {
        new: true,
        runValidators: true,
      },
    );
  }

  async remove(directionId: number): Promise<Direction> {
    return await this.directionModel.findOneAndDelete({ directionId });
  }
}
