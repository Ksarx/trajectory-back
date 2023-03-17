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

  async findAll(): Promise<Direction[]> {
    return await this.directionModel.find();
  }

  async findOne(id: number): Promise<Direction> {
    const direction = await this.directionModel.findOne({ id });

    if (!direction) {
      throw new NotFoundException('Direction not found.');
    }

    return direction;
  }

  async findJobDirections(idJob: number): Promise<Direction[]> {
    const directions = await this.directionModel.find({ idJobs: idJob });

    if (!directions) {
      throw new NotFoundException('Directions not found.');
    }

    return directions;
  }

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
