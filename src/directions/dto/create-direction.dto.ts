export class CreateDirectionDto {
  readonly code: string;
  readonly name: string;
  readonly level: string;
  readonly faculty: string;
  readonly profile: string;
  readonly description: string;
  readonly idJobs: number[];
  readonly semesters: {
    semNumber: number;
    disciplines: string[];
  }[];
}
